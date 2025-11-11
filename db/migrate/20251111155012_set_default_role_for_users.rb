class SetDefaultRoleForUsers < ActiveRecord::Migration[8.0]
  class MigrationUser < ActiveRecord::Base
    self.table_name = "users"
  end

  def up
    change_column_default :users, :role, from: nil, to: "user"

    say_with_time "Backfilling user roles" do
      MigrationUser.where(role: [nil, ""]).update_all(role: "user")
    end

    change_column_null :users, :role, false, "user"
  end

  def down
    change_column_null :users, :role, true
    change_column_default :users, :role, from: "user", to: nil
  end
end
