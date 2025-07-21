class RenameProductFields < ActiveRecord::Migration[7.1]
  def change
    rename_column :products, :название, :name
    rename_column :products, :цена, :price
  end
end
