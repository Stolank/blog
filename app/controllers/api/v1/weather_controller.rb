require "httparty"

module Api
  module V1
    class WeatherController < Api::BaseController 
      def show 
        city = params[:city] || "Almaty"

        api_key = "c16bd751dc76b41135a5492ec678814e"

        response = HTTParty.get(
          "https://api.openweathermap.org/data/2.5/weather",
          query: {
            q: city,
            appid: api_key,
            units: "metric",
            lang: "ru"
          }
        )

          data = response.parsed_response 

           if response.code == 200
          render json: {
            город: data["name"],
            температура: data.dig("main", "temp"),
            ощущается_как: data.dig("main", "feels_like"),
            погода: data.dig("weather", 0, "description"),
            ветер: "#{data.dig("wind", "speed")} м/с",
            влажность: "#{data.dig("main", "humidity")}%",
            давление: "#{data.dig("main", "pressure")} гПа"
          }
        else
          render json: {
            ошибка: data["message"] || "Ошибка запроса к погодному API",
            код: response.code
          }, status: :bad_gateway
        end
      end
    end
  end
end
