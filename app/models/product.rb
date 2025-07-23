class Product < ApplicationRecord
  validates :name, presence: true
  validates :price, presence: true, numericality: { only_integer: true }
  
  validates :name, presence: true
  validates :price, numericality: { greater_than: 0 }
end
