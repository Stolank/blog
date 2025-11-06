class WeatherController < ApplicationController
  def index
    @city = params[:city].presence || "Almaty"
    @weather = WeatherService.fetch_weather(@city)
  end
end