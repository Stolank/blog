class City < ApplicationRecord
  validates :name, presence: true
  validates :country, presence: true
  validates :last_temp, presence: true
end
