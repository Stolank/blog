Rails.application.routes.draw do
  root "home#index"             # Главная
  get "news", to: "news#index"   # Новости 
  get "home/index"
  

  namespace :api, defaults: { format: :json } do  # Пространство имён для API
    resources :products, only: [:index, :create, :destroy, :update]    # Маршруты для продуктов
  end
end