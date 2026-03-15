import request from '../utils/request'

/**
 * 站点管理相关API
 */
export const sitesApi = {
  /**
   * 获取站点列表
   * @param {number} page - 页码
   * @param {number} size - 每页数量
   * @returns {Promise} 站点列表
   */
  async getSites(page = 1, size = 10) {
    const response = await request.get('/v1/sites/')
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 获取单个站点
   * @param {number} id - 站点ID
   * @returns {Promise} 站点详情
   */
  async getSite(id) {
    const response = await request.get(`/v1/sites/${id}`)
    return response.data
  },

  /**
   * 创建站点
   * @param {Object} siteData - 站点数据
   * @returns {Promise} 创建结果
   */
  async createSite(siteData) {
    const response = await request.post('/v1/sites/', siteData)
    return response.data
  },

  /**
   * 更新站点
   * @param {number} id - 站点ID
   * @param {Object} siteData - 站点数据
   * @returns {Promise} 更新结果
   */
  async updateSite(id, siteData) {
    const response = await request.put(`/v1/sites/${id}`, siteData)
    return response.data
  },

  /**
   * 删除站点
   * @param {number} id - 站点ID
   * @returns {Promise} 删除结果
   */
  async deleteSite(id) {
    const response = await request.delete(`/v1/sites/${id}`)
    return response.data
  }
}

export default sitesApi