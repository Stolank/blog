FactoryBot.define do 
  factory :user do
    email { "user@example.com" }
    password { "password123" }
    admin { false }
  end


  factory :admin, class: "User" do
    email { "admin@example.com"}
    password { "password123" }
    admin { true }
  end
end

