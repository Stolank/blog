Rails.application.routes.draw do
  devise_for :users
  root "pages#home"
  get "weather", to: "weather#index"

  namespace :admin do
    get "dashboard", to: "dashboard#index"
  end

  resources :cities
  resources :articles

  get    "/login",  to: "sessions#new"
  post   "/login",  to: "sessions#create"
  delete "/logout", to: "sessions#destroy"

  
  namespace :api do
    namespace :v1 do
      resources :comments, only: [:index]
      resources :articles, only: %i[index show]
      resources :cities,   only: %i[index show]

      get "weather", to: "weather#show"
    end
  end
end