import { message } from 'antd';
import { getKnowledge, editKnowledge, getMedias, rmMedias } from '@/services/admin';

export default {
  namespace: 'knowledge',

  state: {
    online: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    bookCate: [],
    books: {},
    blogList: [],
    blogContent: {},
    mediaItems: [],
    editResult: undefined,
  },

  effects: {
    *getBooks({ op, action, payload }, { call, put }) {
      const response = yield call(getKnowledge, op, action, payload);
      yield put({
        type: 'saveBooks',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *getOnline({ op, action, payload }, { call, put }) {
      const response = yield call(getKnowledge, op, action, payload);
      yield put({
        type: 'saveData',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *getMedias(_, { call, put }) {
      const response = yield call(getMedias);
      yield put({
        type: 'save',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *editBooks({ op, action, payload, callback }, { call, put }) {
      const response = yield call(editKnowledge, op, action, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
    *rmMedias({ payload }, { call, put }) {
      const response = yield call(rmMedias, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
    },
  },

  reducers: {
    save(state, { payload }) {
      return {
        ...state,
        mediaItems: payload,
      };
    },
    saveBooks(state, { payload }) {
      return {
        ...state,
        ...payload,
      };
    },
    saveData(state, { payload }) {
      return {
        ...state,
        online: payload,
      };
    },
    editStatus(state, { payload }) {
      if (payload && payload.status === 'SUCCESS' && payload.data !== 'media') {
        message.success(payload.message);
      } else if (payload && payload.data !== 'media') {
        message.error(payload && payload.message);
      }
      return {
        ...state,
        editResult: payload,
      };
    },
  },
};
