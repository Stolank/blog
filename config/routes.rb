Rails.application.routes.draw do
  root "pages#home"

  devise_for :users

  get "weather", to: "weather#index"

  get "/login", to: redirect("/users/sign_in", status: 302)

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
