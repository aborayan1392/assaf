// اسم ذاكرة التخزين المؤقت (Cache)
const CACHE_NAME = 'class-management-cache-v1';

// قائمة الملفات التي سيتم تخزينها
const urlsToCache = [
  './ادارة الصف.html',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap'
];

// 1. تثبيت الـ Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// 2. تفعيل الـ Service Worker (يمكن استخدامه لاحقًا لتنظيف الـ Cache القديم)
self.addEventListener('activate', event => {
    // يمكنك إضافة منطق تنظيف الـ Cache هنا في المستقبل
    console.log('Service worker activated');
});

// 3. اعتراض طلبات الشبكة (Fetch)
// هذا هو الجزء الذي يجعل التطبيق يعمل دون اتصال
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // إذا وُجد الطلب في الـ Cache، قم بإرجاعه
        if (response) {
          return response;
        }
        // إذا لم يُوجد، اذهب إلى الشبكة للحصول عليه
        return fetch(event.request);
      })
  );
});