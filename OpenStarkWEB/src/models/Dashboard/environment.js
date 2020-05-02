import { message } from 'antd';
import { getEnv, editEnv } from '@/services/admin';

export default {
  namespace: 'environment',

  state: {
    envList: {
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
    *fetchEnv({ op, action, payload }, { call, put }) {
      const response = yield call(getEnv, op, action, payload);
      yield put({
        type: 'save',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchEnvDetail({ op, action, payload }, { call, put }) {
      const response = yield call(getEnv, op, action, payload);
      yield put({
        type: 'saveDetail',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *editEnv({ op, action, payload, callback }, { call, put }) {
      const response = yield call(editEnv, op, action, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
  },

  reducers: {
    save(state, { payload }) {
      return {
        ...state,
        envList: payload,
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
