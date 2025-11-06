module Api
  module V1
    class CitiesController < ApplicationController
      def index
        scope = City.order(:name)
        if params[:q].present?
          q = "%#{params[:q]}%"
          scope = scope.where("name LIKE ? OR country LIKE ?", q, q)
        end
        items, meta = paginate(scope)
        render json: { data: items.as_json(only: %i[id name country]), meta: meta }
      end

      def show
        city = City.find(params[:id])
        render json: { data: city.as_json(only: %i[id name country]) }
      end

      private
      
      def record_not_found
        render json: { error: "City not found" }, status: :not_found
      end
    end
  end
end