import request from '../utils/request'

/**
 * 省份城市管理相关API
 */
export const geoApi = {
  /**
   * 获取省份列表
   * @returns {Promise} 省份列表
   */
  async getProvinces() {
    const response = await request.get('/v1/geo/provinces')
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 创建省份
   * @param {Object} data - 省份数据
   * @returns {Promise} 创建结果
   */
  async createProvince(data) {
    const response = await request.post('/v1/geo/provinces', data)
    return response.data
  },

  /**
   * 更新省份
   * @param {number} id - 省份ID
   * @param {Object} data - 更新数据
   * @returns {Promise} 更新结果
   */
  async updateProvince(id, data) {
    const response = await request.put(`/v1/geo/provinces/${id}`, data)
    return response.data
  },

  /**
   * 删除省份
   * @param {number} id - 省份ID
   * @returns {Promise} 删除结果
   */
  async deleteProvince(id) {
    const response = await request.delete(`/v1/geo/provinces/${id}`)
    return response.data
  },

  /**
   * 获取城市列表
   * @param {number} provinceId - 省份ID（可选）
   * @returns {Promise} 城市列表
   */
  async getCities(provinceId = null) {
    const params = {}
    if (provinceId) {
      params.province_id = provinceId
    }
    const response = await request.get('/v1/geo/cities', { params })
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 创建城市
   * @param {Object} data - 城市数据
   * @returns {Promise} 创建结果
   */
  async createCity(data) {
    const response = await request.post('/v1/geo/cities', data)
    return response.data
  },

  /**
   * 更新城市
   * @param {number} id - 城市ID
   * @param {Object} data - 更新数据
   * @returns {Promise} 更新结果
   */
  async updateCity(id, data) {
    const response = await request.put(`/v1/geo/cities/${id}`, data)
    return response.data
  },

  /**
   * 删除城市
   * @param {number} id - 城市ID
   * @returns {Promise} 删除结果
   */
  async deleteCity(id) {
    const response = await request.delete(`/v1/geo/cities/${id}`)
    return response.data
  },

  /**
   * 获取省份城市树形结构
   * @returns {Promise} 树形结构数据
   */
  async getGeoTree() {
    const response = await request.get('/v1/geo/tree')
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 获取区县列表
   * @param {number} cityId - 城市ID（可选）
   * @returns {Promise} 区县列表
   */
  async getDistricts(cityId = null) {
    const params = {}
    if (cityId) {
      params.city_id = cityId
    }
    const response = await request.get('/v1/geo/districts', { params })
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 创建区县
   * @param {Object} data - 区县数据
   * @returns {Promise} 创建结果
   */
  async createDistrict(data) {
    const response = await request.post('/v1/geo/districts', data)
    return response.data
  },

  /**
   * 更新区县
   * @param {number} id - 区县ID
   * @param {Object} data - 更新数据
   * @returns {Promise} 更新结果
   */
  async updateDistrict(id, data) {
    const response = await request.put(`/v1/geo/districts/${id}`, data)
    return response.data
  },

  /**
   * 删除区县
   * @param {number} id - 区县ID
   * @returns {Promise} 删除结果
   */
  async deleteDistrict(id) {
    const response = await request.delete(`/v1/geo/districts/${id}`)
    return response.data
  }
}

export default geoApi
