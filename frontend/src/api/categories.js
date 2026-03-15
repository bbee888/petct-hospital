import request from '../utils/request'

/**
 * 栏目管理相关API
 */
export const categoriesApi = {
  /**
   * 获取栏目列表
   * @returns {Promise} 栏目列表
   */
  async getCategories() {
    const response = await request.get('/v1/articles/categories')
    return response.data || []
  },

  /**
   * 创建分类
   * @param {Object} data - 分类数据
   * @returns {Promise} 创建结果
   */
  async createCategory(data) {
    const response = await request.post('/v1/articles/categories', data)
    return response.data
  },

  /**
   * 更新分类
   * @param {number} id - 分类ID
   * @param {Object} data - 分类数据
   * @returns {Promise} 更新结果
   */
  async updateCategory(id, data) {
    const response = await request.put(`/v1/articles/categories/${id}`, data)
    return response.data
  },

  /**
   * 删除分类
   * @param {number} id - 分类ID
   * @returns {Promise} 删除结果
   */
  async deleteCategory(id) {
    const response = await request.delete(`/v1/articles/categories/${id}`)
    return response.data
  }
}

export default categoriesApi
