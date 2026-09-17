// study-ai worker — 유란시아서 스터디 에디션의 AI 기능(번역 비교·난해절 해설·강론쓰기·단어 정리)을
// 대신 처리하는 클라우드플레어 워커. 넷리파이 함수(/.netlify/functions/study-ai)를 대체한다.
//
// 배포 방법:
//   1) dash.cloudflare.com → Workers & Pages → Create → Worker 이름 입력(예: urantia-study-ai)
//   2) 코드 편집 화면에 이 파일 내용을 통째로 붙여넣고 Deploy
//   3) Settings → Variables and Secrets → Add → 이름 ANTHROPIC_API_KEY, 값에 실제 API 키 입력(Secret으로 저장)
//   4) 배포된 워커 주소(예: https://urantia-study-ai.<계정>.workers.dev)를 study/index.html의
//      AI_ENDPOINT 두 곳에 넣고 다시 커밋·푸시

const MODEL = "claude-sonnet-4-6";
const MAX_TOKENS = 1500;

const SYSTEM_PROMPTS = {
  compare: `너는 유란시아서(The Urantia Book) 한국어판과 영어 원문을 나란히 놓고 살펴보는 번역 비교 도우미다.
주어진 절의 한국어 번역과 영어 원문을 비교해서, 다음을 짧고 명확한 한국어로 정리해라.
1) 핵심 용어나 표현 중 번역 선택이 갈릴 수 있는 지점
2) 한국어판이 영어 뉘앙스를 놓쳤거나 다르게 살린 부분(있다면)
3) 원문을 더 깊이 이해하는 데 도움이 되는 짧은 한마디
과장하거나 번역이 틀렸다고 단정하지 말고, 연구자가 스스로 판단할 수 있도록 근거를 담아 설명해라. 250~400자 내외로 답하고, 별표(*)는 쓰지 마라.`,

  explain: `너는 유란시아서를 연구하는 사람을 돕는 해설자다.
주어진 절이 왜 난해하게 느껴질 수 있는지, 핵심 개념과 맥락을 평이한 한국어로 풀어서 설명해라.
전문 용어가 나오면 한 문장으로 풀어주고, 이 절이 속한 편의 전체 흐름 속에서 어떤 역할을 하는지도 한 문단으로 짚어줘라.
확실하지 않은 추정은 추정이라고 밝히고, 단정적인 신학적 결론을 내리지 마라. 300~450자 내외, 별표(*) 없이 답해라.`,

  sermon: `너는 유란시아서를 기반으로 한 강론(설교/발표) 초안을 잡아주는 도우미다.
주어진 절 본문과(있다면) 사용자의 메모를 바탕으로, 청중에게 전할 수 있는 짧은 강론 초안을 한국어로 작성해라.
구성은 ①본문이 말하는 핵심 ②오늘의 삶에 어떻게 이어지는지 ③마무리 권면, 이렇게 자연스러운 산문으로 쓰고
소제목이나 번호는 달지 마라. 감동을 준다고 해서 본문에 없는 내용을 지어내지 말고, 사용자의 메모가 있으면 그 방향을 최우선으로 반영해라.
400~700자 내외, 별표(*) 없이 답해라.`,

  word: `너는 유란시아서에 나오는 개념·용어를 정리해주는 도우미다.
주어진 단어와(있다면) 그 단어가 쓰인 한국어 예문을 참고해서, 이 단어가 유란시아서 안에서 어떤 의미로 쓰이는지
짧고 명확하게 정리해라. 일반 사전적 의미와 다르게 쓰이는 지점이 있다면 반드시 짚어주고,
확실치 않으면 확실치 않다고 밝혀라. 200~350자 내외, 별표(*) 없이 답해라.`,
};

function buildUserMessage(mode, payload) {
  payload = payload || {};
  if (mode === "compare") {
    return `절번호: ${payload.ref || "(미상)"}\n한국어: ${payload.ko || ""}\n영어 원문: ${payload.en || ""}`;
  }
  if (mode === "explain") {
    return `절번호: ${payload.ref || "(미상)"}\n본문: ${payload.ko || ""}`;
  }
  if (mode === "sermon") {
    const loc = [payload.paper, payload.section].filter(Boolean).join(" - ");
    let msg = `편/장: ${loc || "(미상)"}\n본문: ${payload.ko || ""}`;
    if (payload.notes) msg += `\n사용자 메모: ${payload.notes}`;
    return msg;
  }
  if (mode === "word") {
    let msg = `단어: ${payload.word || ""}`;
    if (payload.ko) msg += `\n쓰인 예문: ${payload.ko}`;
    return msg;
  }
  return JSON.stringify(payload);
}

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "content-type",
};

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }
    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "POST만 지원합니다." }), {
        status: 405,
        headers: { "content-type": "application/json", ...CORS_HEADERS },
      });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response(JSON.stringify({ error: "잘못된 요청입니다." }), {
        status: 400,
        headers: { "content-type": "application/json", ...CORS_HEADERS },
      });
    }

    const { mode, payload } = body || {};
    const system = SYSTEM_PROMPTS[mode];
    if (!system) {
      return new Response(JSON.stringify({ error: `알 수 없는 모드: ${mode}` }), {
        status: 400,
        headers: { "content-type": "application/json", ...CORS_HEADERS },
      });
    }

    if (!env.ANTHROPIC_API_KEY) {
      return new Response(JSON.stringify({ error: "서버에 API 키가 설정되지 않았습니다." }), {
        status: 500,
        headers: { "content-type": "application/json", ...CORS_HEADERS },
      });
    }

    const userMessage = buildUserMessage(mode, payload);

    try {
      const resp = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "x-api-key": env.ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model: MODEL,
          max_tokens: MAX_TOKENS,
          system,
          messages: [{ role: "user", content: userMessage }],
        }),
      });

      const data = await resp.json();

      if (!resp.ok) {
        return new Response(JSON.stringify({ error: data }), {
          status: resp.status,
          headers: { "content-type": "application/json", ...CORS_HEADERS },
        });
      }

      const text = (data.content || [])
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join("\n")
        .trim();

      return new Response(JSON.stringify({ text }), {
        headers: { "content-type": "application/json", ...CORS_HEADERS },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: String(err) }), {
        status: 502,
        headers: { "content-type": "application/json", ...CORS_HEADERS },
      });
    }
  },
};
