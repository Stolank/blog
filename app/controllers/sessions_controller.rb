class SessionsController < ApplicationController
  def new
  end

  def create
    user = User.find_by(email: params[:email])
    if user
      session[:user_id] = user.id
      redirect_to root_path, notice: "Вход выполнен как #{user.name} (#{user.role})."
    else
      flash.now[:alert] = "Пользователь с таким email не найден."
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    reset_session
    redirect_to root_path, notice: "Вы вышли из аккаунта."
  end
end