module Api
  module V1
    class ApplicationController < ActionController::API
      private

      def paginate(scope)
        page  = (params[:page] || 1).to_i
        per   = (params[:per]  || 10).to_i
        per   = 100 if per > 100

        total = scope.count
        pages = (total / per.to_f).ceil
        items = scope.offset((page - 1) * per).limit(per)

        [items, { page: page, per: per, total: total, pages: pages }]
      end
    end
  end
end