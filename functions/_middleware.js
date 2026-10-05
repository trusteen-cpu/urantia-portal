// 임시 닫기 (2026-10-05): urantiareaders.com 으로 들어오는 요청은 모두 404.
// 관리자는 Cloudflare 내부 주소 urantia-portal.pages.dev 로 계속 볼 수 있다.
// 다시 열 때는 이 파일(functions/_middleware.js)을 지우고 푸시하면 된다.
const PAGE = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>404 Not Found</title>
<style>body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#333;margin:0;padding:60px 20px;text-align:center}h1{font-weight:600;font-size:28px;margin:0 0 12px}hr{border:0;border-top:1px solid #ddd;max-width:420px;margin:18px auto}p{color:#888;font-size:14px}</style>
</head><body><h1>404 Not Found</h1><hr><p>The requested URL was not found on this server.</p></body></html>`;

export async function onRequest(ctx) {
  const host = new URL(ctx.request.url).hostname;
  if (host.endsWith(".pages.dev")) return ctx.next();
  return new Response(PAGE, {
    status: 404,
    headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" },
  });
}
