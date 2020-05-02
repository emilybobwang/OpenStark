import { message } from 'antd';
import {
  fetchChartData,
  fetchLoadData,
  fetchLoadAPI,
  editLoadAPI,
  fetchTestData,
} from '@/services/admin';

export default {
  namespace: 'chart',

  state: {
    toolsPVRange: [],
    toolsActiveRange: [],
    toolsPVRanking: [],
    toolsActiveRanking: [],
    toolsRangeData: [],
    toolsList: [],
    loadNames: {},
    loadData: [],
    loadEvn: [],
    apiList: {
      page: 1,
      size: 10,
      total: 0,
      data: [],
    },
    guiCaseData: {},
    apiCaseData: {},
    caseStatus: {},
    guiJobs: [],
    guiReports: [],
    apiJobs: [],
    apiReports: [],
    dockerList: [],
    guiJacoco: [],
    apiJacoco: [],
  },

  effects: {
    *fetch({ payload }, { call, put }) {
      const response = yield call(fetchChartData, payload);
      yield put({
        type: 'save',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchLoad({ payload }, { call, put }) {
      const response = yield call(fetchLoadData, payload);
      yield put({
        type: 'save',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchLoadAPI({ op, payload }, { call, put }) {
      const response = yield call(fetchLoadAPI, op, payload);
      yield put({
        type: 'saveAPI',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchDocker({ op, action, payload }, { call, put }) {
      const response = yield call(fetchTestData, op, action, payload);
      yield put({
        type: 'saveDocker',
        payload: response && typeof Array.isArray(response.data) ? response.data : [],
      });
    },
    *fetchTestData({ op, action, payload }, { call, put }) {
      const response = yield call(fetchTestData, op, action, payload);
      yield put({
        type: 'save',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *editLoadAPI({ op, payload }, { call }) {
      const response = yield call(editLoadAPI, op, payload);
      if (response && response.status === 'SUCCESS') {
        message.success(response.message);
      } else {
        message.error(response && response.message);
      }
    },
  },

  reducers: {
    save(state, { payload }) {
      return {
        ...state,
        ...payload,
      };
    },
    saveAPI(state, { payload }) {
      return {
        ...state,
        apiList: payload,
      };
    },
    saveDocker(state, { payload }) {
      return {
        ...state,
        dockerList: payload,
      };
    },
    clear() {
      return {
        toolsPVRange: [],
        toolsActiveRange: [],
        toolsPVRanking: [],
        toolsActiveRanking: [],
        toolsRangeData: [],
        toolsList: [],
        loadNames: {},
        loadData: [],
        loadEvn: [],
        guiCaseData: {},
        apiCaseData: {},
        caseStatus: {},
        guiJobs: [],
        guiReports: [],
        apiJobs: [],
        apiReports: [],
        dockerList: [],
        guiJacoco: [],
        apiJacoco: [],
      };
    },
  },
};
