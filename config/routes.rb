Rails.application.routes.draw do
  root "home#index"
  get "home/index"
  get "home/about", to: "home#about", as: "about"

  namespace :api do
    resources :products, only: [:index, :create]
  end
end