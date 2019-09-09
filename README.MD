Budowa obrazu dockera (w folderze projektu):
sudo docker build -t microservice-flask .
Uruchomienie obrazu:
sudo docker run -d -p 5000:5000 microservice-flask

Lista przykładowych żądań do systemu API:
- HTTP GET http://127.0.0.1:5000/list-text-ids - zwraca wszystkie id zapisanych tekstów
- HTTP GET http://127.0.0.1:5000/list-images-ids - zwraca wszystkie id stron dla których pobrano obrazki
- HTTP GET http://127.0.0.1:5000/images/c27334cc-950f-4e5c-a420-c8756a3dfe51 - zwraca wszystkie linki do obrazków przechowywanych w systemie dla danego zasobu
- HTTP GET http://127.0.0.1:5000/text/3dbee8df-e326-4244-b884-816944ce13f7 - zwraca tekst dla danego zasobu 
- HTTP GET http://127.0.0.1:5000/images-id/00554e7f-44cb-4675-a955-39fc065bb212/image/koalicja-rozowa-960x252-Showcase.jpg - zwraca konkretny obrazek z systemu 
- HTTP POST http://127.0.0.1:5000/scrape-text -  z ciałem w postaci json {"url":"<url_do_strony>"} i nagłówkiem 'Content-Type: application/json'
curl -X POST -H 'Content-Type: application/json' -i 'http://127.0.0.1:5000/scrape-text' --data '{"url":"https://www.geeksforgeeks.org/"}' - pobiera text z podanego url
- HTTP POST http://127.0.0.1:5000/scrape-images -  z ciałem w postaci json {"url":"<url_do_strony>"} i nagłówkiem 'Content-Type: application/json'
curl -X POST -H 'Content-Type: application/json' -i 'http://127.0.0.1:5000/scrape-images' --data '{"url":"https://www.geeksforgeeks.org/"}' - pobiera wszystkie obrazki z podanego url

Uruchomienie testów: python3 tests/Tests.py