import { queryActivities } from '@/services/admin';

export default {
  namespace: 'activities',

  state: {
    list: [],
    blogs: [],
    users: [],
  },

  effects: {
    *fetchList(_, { call, put }) {
      const response = yield call(queryActivities);
      yield put({
        type: 'saveList',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
  },

  reducers: {
    saveList(state, { payload }) {
      return {
        ...state,
        list: payload.active || [],
        blogs: payload.blogs || [],
        users: payload.users || [],
      };
    },
  },
};
