class Comment < ApplicationRecord
  # Это ссылка на родителя к
  belongs_to :parent, class_name: "Comment", optional: true

  # это список на детей 
  has_many :children, class_name: "Comment", foreign_key: "parent_id", dependent: :destroy
end
