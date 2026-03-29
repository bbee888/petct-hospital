import request from '../utils/request'

/**
 * 医院管理相关API
 */
export const hospitalsApi = {
  /**
   * 获取医院列表
   * @param {number} page - 页码
   * @param {number} size - 每页数量
   * @param {string} search - 搜索关键词
   * @returns {Promise} 医院列表
   */
  async getHospitals(page = 1, size = 10, search = '') {
    const response = await request.get('/v1/hospitals/', {
      params: { page, size, search }
    })
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 获取单个医院
   * @param {number} id - 医院ID
   * @returns {Promise} 医院详情
   */
  async getHospital(id) {
    const response = await request.get(`/v1/hospitals/${id}`)
    return response.data
  },

  /**
   * 创建医院
   * @param {Object} hospitalData - 医院数据
   * @returns {Promise} 创建结果
   */
  async createHospital(hospitalData) {
    const response = await request.post('/v1/hospitals/', hospitalData)
    return response.data
  },

  /**
   * 更新医院
   * @param {number} id - 医院ID
   * @param {Object} hospitalData - 医院数据
   * @returns {Promise} 更新结果
   */
  async updateHospital(id, hospitalData) {
    const response = await request.put(`/v1/hospitals/${id}`, hospitalData)
    return response.data
  },

  /**
   * 删除医院
   * @param {number} id - 医院 ID
   * @returns {Promise} 删除结果
   */
  async deleteHospital(id) {
    const response = await request.delete(`/v1/hospitals/${id}`)
    return response.data
  },

  /**
   * 获取合作医院数量统计
   * @returns {Promise} 合作医院数量
   */
  async getCooperationCount() {
    const response = await request.get('/v1/stats/hospitals/cooperation')
    return response.data
  }
}

export default hospitalsApi