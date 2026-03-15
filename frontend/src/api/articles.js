import request from '../utils/request'

/**
 * 文章管理相关API
 */
export const articlesApi = {
  /**
   * 获取文章列表
   * @param {number} page - 页码
   * @param {number} size - 每页数量
   * @param {string} search - 搜索关键词
   * @returns {Promise} 文章列表
   */
  async getArticles(page = 1, size = 10, search = '') {
    const response = await request.get('/v1/articles/', {
      params: { page, size, search }
    })
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 获取单个文章
   * @param {number} id - 文章ID
   * @returns {Promise} 文章详情
   */
  async getArticle(id) {
    const response = await request.get(`/v1/articles/${id}`)
    return response.data
  },

  /**
   * 创建文章
   * @param {Object} articleData - 文章数据
   * @returns {Promise} 创建结果
   */
  async createArticle(articleData) {
    const response = await request.post('/v1/articles/', articleData)
    return response.data
  },

  /**
   * 更新文章
   * @param {number} id - 文章ID
   * @param {Object} articleData - 文章数据
   * @returns {Promise} 更新结果
   */
  async updateArticle(id, articleData) {
    const response = await request.put(`/v1/articles/${id}`, articleData)
    return response.data
  },

  /**
   * 删除文章
   * @param {number} id - 文章ID
   * @returns {Promise} 删除结果
   */
  async deleteArticle(id) {
    const response = await request.delete(`/v1/articles/${id}`)
    return response.data
  }
}

export default articlesApi