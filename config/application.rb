require_relative "boot"

require "rails/all"

# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

module Blog
  class Application < Rails::Application
    config.load_defaults 8.0
    config.api_key = "SECRET123"   # наш API-ключ

    config.autoload_lib(ignore: %w[assets tasks])
  end
end
