#!/bin/sh
# الاستخدام: ./set-domain.sh example.com [pub-1234567890123456]
D="$1"; [ -z "$D" ] && { echo "اكتب الدومين: ./set-domain.sh example.com"; exit 1; }
cd "$(dirname "$0")/public" || exit 1
sed -i "s/__DOMAIN__/$D/g" *.html
echo "$D" > CNAME
printf 'User-agent: *\nAllow: /\nSitemap: https://%s/sitemap.xml\n' "$D" > robots.txt
{ printf '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  for p in "" about contact privacy terms cookies pdf-to-word word-to-pdf image-to-pdf jpg-to-pdf excel-to-pdf pdf-to-image pdf-to-jpg merge-pdf pdf-to-text image-to-text; do printf '<url><loc>https://%s/%s</loc></url>' "$D" "$p"; done
  printf '</urlset>'; } > sitemap.xml
[ -n "$2" ] && echo "google.com, $2, DIRECT, f08c47fec0942fa0" > ads.txt
echo "تم. ارفع محتوى مجلد public إلى GitHub."
