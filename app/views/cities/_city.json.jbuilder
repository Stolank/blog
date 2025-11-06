json.extract! city, :id, :name, :country, :last_temp, :created_at, :updated_at
json.url city_url(city, format: :json)
