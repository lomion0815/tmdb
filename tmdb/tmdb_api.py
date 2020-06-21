import requests

class Connection():
    def __init__(self):
        self.load_parameters()
        
    def load_parameters(self):
        self.api_key = '51d75c00dc1502dc894b7773ec3e7a15'
        
        self.base_url = "https://api.themoviedb.org/3/"
        result = requests.get(self.base_url + 'configuration', params = self.get_apikey()).json()
        self.base_url_poster = result['images']['base_url'] + result['images']['poster_sizes'][0]
        self.valid = False

    def get_apikey(self):
        return { 'api_key' : self.api_key }

    def request(self, id):
        url = self.base_url+ 'movie/' + str(id)
        payload = self.get_apikey()
        payload['language'] = 'de'
        result = requests.get(url, params=payload)
        self.valid = True
        return result

    def get_image_binary(self):
        return requests.get(self.poster_url).content


class Movie(Connection):
    def __init__(self):
        self.load_parameters()
        pass
        
    def search_title(self, title):
        url = self.base_url+ 'search/movie'
        payload = self.get_apikey()
        payload['language'] = 'de'
        payload['query'] = title
        result = requests.get(url, params=payload)
        json = result.json()
        if json['total_results'] > 0:
            self.query_details(json['results'][0]['id'])

    def query_details(self, id):
        data = self.request(id).json()
        self.title = data['title']
        self.poster_url = self.base_url_poster + data['poster_path']
        self.overview = data['overview']
        self.web_url = 'https://www.themoviedb.org/movie/' + str(data['id'])
        self.vote_average = str(data['vote_average'])
        
        
movie = Movie()
#movie.query_details('550')
movie.search_title('Jack Reacher')
print(movie.title)
print(movie.overview[:150])
print(movie.web_url)
print(movie.poster_url)
