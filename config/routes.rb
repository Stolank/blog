Rails.application.routes.draw do
  root "pages#home"

  devise_for :users

  get "weather", to: "weather#index"

  get    "/login",  to: "sessions#new"
  post   "/login",  to: "sessions#create"
  delete "/logout", to: "sessions#destroy"

  namespace :admin do
    get "dashboard", to: "dashboard#index"
  end
  # CRUD
  resources :cities
  resources :articles

  # API
  namespace :api do
    namespace :v1 do
      resources :comments, only: [:index]
      resources :articles, only: %i[index show]
      resources :cities,   only: %i[index show]

      get "weather", to: "weather#show"
    end
  end
end
