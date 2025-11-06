class CreateCities < ActiveRecord::Migration[8.0]
  def change
    create_table :cities do |t|
      t.string :name
      t.string :country
      t.float :last_temp

      t.timestamps
    end
  end
end
