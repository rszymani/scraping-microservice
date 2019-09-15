Project is a simple API to scrape text and images from any site.  

To build docker execute command:
docker-compose build
To run docker execute command:
docker-compose up

List of example api request:
- HTTP GET http://127.0.0.1:5000/textIDs - returns all possible text IDs
- HTTP GET http://127.0.0.1:5000/imagesIDs - returns all possible images IDs
- HTTP GET http://127.0.0.1:5000/images/c27334cc-950f-4e5c-a420-c8756a3dfe51 - returns all images under specific UUID (from one site)
- HTTP GET http://127.0.0.1:5000/text/3dbee8df-e326-4244-b884-816944ce13f7 - return text for site with exmample ID 
- HTTP GET http://127.0.0.1:5000/images-id/00554e7f-44cb-4675-a955-39fc065bb212/image/koalicja-rozowa-960x252-Showcase.jpg - returns image content for example image
- HTTP POST http://127.0.0.1:5000/scrapeText -  z ciałem w postaci json {"url":"<url_to_site>"} with header 'Content-Type: application/json'
curl -X POST -H 'Content-Type: application/json' -i 'http://127.0.0.1:5000/scrape-text' --data '{"url":"https://www.geeksforgeeks.org/"}' - scrape text from requested site (url in body)
- HTTP POST http://127.0.0.1:5000/scrapeImages -  z ciałem w postaci json {"url":"<url_to_site>"} i nagłówkiem 'Content-Type: application/json'
curl -X POST -H 'Content-Type: application/json' -i 'http://127.0.0.1:5000/scrape-images' --data '{"url":"https://www.geeksforgeeks.org/"}' - downloads all images from requested site (url in body)

