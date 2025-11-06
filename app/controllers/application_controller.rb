class ApplicationController < ActionController::Base
  # Разрешаем использование этих методов во view
  helper_method :current_user, :logged_in?, :admin?

  rescue_from ActiveRecord::RecordNotFound, with: :record_not_found
  rescue_from ActionController::ParameterMissing, with: :bad_request
 
  private

  
  # Авторизация
  def current_user
    return @current_user if defined?(@current_user)
    @current_user ||= User.find_by(id: session[:user_id])
  end

  def logged_in?
    current_user.present?
  end

  def admin?
    current_user&.admin?
  end

  private

  def require_login
    unless logged_in?
      respond_to do |format|
        format.html { redirect_to login_path, alert: "Нужен вход в систему" }
        format.json { render json: { error: "Authentication required" }, status: :unauthorized }
      end
    end
  end

  def require_admin
    unless admin?
      format_to do |format|
        format.html { redirect_to root_path, alert "Недостаточно прав (только для администратора)." }
        format.json { render json: { error: "Admin access requred" }, status: :forbidden }
      end
    end
  end

  # Обработка ошибок 
  def record_not_found(exception)
    respond_to do |format|
      format.html { redirect_to root_path, alert: "Запись не найдена" }
      format.json { render json: { error: "Record not found", details: exception.message } status: :not_found}
    end
  end

  def bad_request(exception)
    render json: { error: "Bad request", details: exception.message }, status: :bad_request
  end

  # Не обязательно но удобно для тестов
   def internal_error(exception)
    render json: { error: "Internal server error", details: exception.message }, status: :internal_server_error
  end
end