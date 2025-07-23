Rails.application.routes.draw do
  root "home#index"
  get "home/index"
  get "home/about", to: "home#about", as: "about"

  namespace :api, defaults: { format: :json } do
    resources :products, only: [:index, :create, :destroy, :update]
  end
end