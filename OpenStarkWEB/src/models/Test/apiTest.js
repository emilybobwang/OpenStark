import { message } from 'antd';
import { getApiTest, editApiTest } from '@/services/test';

export default {
  namespace: 'apiTest',

  state: {
    testCases: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    jobsList: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    reportsList: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    detailList: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    editResult: undefined,
  },

  effects: {
    *fetchApiTest({ op, action, payload }, { call, put }) {
      const response = yield call(getApiTest, op, action, payload);
      yield put({
        type: 'saveData',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchApiJobs({ op, action, payload }, { call, put }) {
      const response = yield call(getApiTest, op, action, payload);
      yield put({
        type: 'saveJobs',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchApiReports({ op, action, payload }, { call, put }) {
      const response = yield call(getApiTest, op, action, payload);
      yield put({
        type: 'saveReports',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchApiDetail({ op, action, payload }, { call, put }) {
      const response = yield call(getApiTest, op, action, payload);
      yield put({
        type: 'saveDetail',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *editApiTest({ op, action, payload, callback }, { call, put }) {
      const response = yield call(editApiTest, op, action, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
  },

  reducers: {
    saveData(state, { payload }) {
      return {
        ...state,
        testCases: payload,
      };
    },
    saveJobs(state, { payload }) {
      return {
        ...state,
        jobsList: payload,
      };
    },
    saveReports(state, { payload }) {
      return {
        ...state,
        reportsList: payload,
      };
    },
    saveDetail(state, { payload }) {
      return {
        ...state,
        detailList: payload,
      };
    },
    editStatus(state, { payload }) {
      if (payload && payload.status === 'SUCCESS') {
        message.success(payload.message);
        if (payload.data.type === 'export' || payload.data.type === 'template') {
          window.location.href = payload.data.url;
        }
      } else {
        message.error(payload && payload.message);
      }
      return {
        ...state,
        editResult: payload,
      };
    },
  },
};
