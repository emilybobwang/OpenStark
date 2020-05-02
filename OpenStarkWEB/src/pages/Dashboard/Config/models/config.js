import { message } from 'antd';
import { fetchConfig, editConfig } from '@/services/admin';

export default {
  namespace: 'config',

  state: {
    configs: {},
    editResult: undefined,
  },

  effects: {
    *fetchConfig(_, { call, put }) {
      const response = yield call(fetchConfig);
      yield put({
        type: 'saveConfig',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *editConfig({ payload, callback }, { call, put }) {
      const response = yield call(editConfig, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
  },

  reducers: {
    saveConfig(state, { payload }) {
      return {
        ...state,
        configs: payload,
      };
    },
    editStatus(state, { payload }) {
      if (payload && payload.data.type === 'navLink') {
        if (payload.status === 'SUCCESS') {
          message.success(payload.message);
        } else {
          message.error(payload && payload.message);
        }
      }
      return {
        ...state,
        editResult: payload,
      };
    },
  },
};
