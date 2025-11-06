module Api
  class BaseController < ActionController::API
    rescue_from ActiveRecord::RecordNotFound, with: :record_not_found

    private

    def paginate_scope(scope)
      page = (params[:page] || 1).to_i
      per  = (params[:per] || 10).to_i

      per = 100 if per > 100
      per = 1 if per < 1
      page = 1 if page < 1 

      paginated = scope.offset((page - 1) * per).limit(per)
      total = scope.count 
      pages = (total / per.to_f).ceil

      {
        items: paginated,
        meta: {
          page: page,
          per: per,
          total: total,
          pages: pages
        }
      }
    end

    def record_not_found(exception)
      render json: {
        error: "Record not found",
        details: exception.message
      }, status: :not_found
    end
  end
end