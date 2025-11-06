
require "httparty"

class WeatherService
  include HTTParty
  base_uri "https://api.openweathermap.org/data/2.5"
  default_timeout 5

  def self.fetch_weather(city)
    api_key = ENV["OPENWEATHER_KEY"] # Ключ положим в переменные окружение 
    
    if api_key.nil? || api_key.strip.empty?
      return {
        "name" => city,
        "main" => { "temp" => 22.0 },
        "weather" => [{ "description" => "demo - add OPENWEATHER_KEY to .env" }]
      }
    end

    resp = get("/weather", query: { q: city, appid: api_key, units: "metric", lang: "ru" })
    resp.parsed_response
    rescue StandardError => e
      {
        "name" => city,
        "main" => {},
        "weather" => [{ "description" => "Ошибка запроса: #{e.class}"}]
      }
    end
  end