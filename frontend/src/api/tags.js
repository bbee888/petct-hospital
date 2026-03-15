import request from '../utils/request'

/**
 * 标签管理相关API
 */
export const tagsApi = {
  /**
   * 获取标签列表
   * @param {number} page - 页码
   * @param {number} size - 每页数量
   * @returns {Promise} 标签列表
   */
  async getTags(page = 1, size = 10) {
    const response = await request.get('/v1/tags/', {
      params: { page, size }
    })
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 创建标签
   * @param {Object} tagData - 标签数据
   * @returns {Promise} 创建结果
   */
  async createTag(tagData) {
    const response = await request.post('/v1/tags/', tagData)
    return response.data
  },

  /**
   * 更新标签
   * @param {number} id - 标签ID
   * @param {Object} tagData - 标签数据
   * @returns {Promise} 更新结果
   */
  async updateTag(id, tagData) {
    const response = await request.put(`/v1/tags/${id}`, tagData)
    return response.data
  },

  /**
   * 删除标签
   * @param {number} id - 标签ID
   * @returns {Promise} 删除结果
   */
  async deleteTag(id) {
    const response = await request.delete(`/v1/tags/${id}`)
    return response.data
  }
}

export default tagsApi