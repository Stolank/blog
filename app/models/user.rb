class User < ApplicationRecord
  # Модули Devise (их добавлял генератор devise)
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable

  # Роли пользователя: обычный user и админ
  # В БД в колонке "role" храним строки "user" или "admin"
  def role 
    read_attribute(:role) || "user"
  end

  # Метод - проверка: админ ли пользователь
  def admin?
    role == "admin"
  end
end
