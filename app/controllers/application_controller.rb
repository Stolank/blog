class ApplicationController < ActionController::Base
  protect_from_forgery with: :null_session

  private

  def authenticate_api_key
    unless params[:api_key] == Rails.application.config.api_key
      render json: { error: "Unauthorized" }, status: :unauthorized
    end
  end
end
