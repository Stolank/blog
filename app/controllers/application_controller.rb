class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception

  private

  def require_admin
    authenticate_user!
    return if current_user&.admin?

    respond_to do |format|
      format.html { redirect_to root_path, alert: "Недостаточно прав для доступа к этой странице." }
      format.json { render json: { error: "Admin access required" }, status: :forbidden }
      format.any  { head :forbidden }
    end
  end
end
