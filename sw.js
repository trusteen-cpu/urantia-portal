/* 아주 가벼운 서비스 워커입니다.
   일부러 fetch 가로채기(캐시)를 하지 않습니다.
   예전에 리더 앱에서 서비스 워커가 옛 파일을 계속 붙들고 있던
   문제를 겪으셨기 때문에, 이 워커는 설치 조건만 만족시킬 뿐
   어떤 파일도 대신 저장해 두지 않습니다. 매번 최신 화면이 뜹니다. */
self.addEventListener('install', function (e) {
  self.skipWaiting();
});
self.addEventListener('activate', function (e) {
  e.waitUntil(self.clients.claim());
});
