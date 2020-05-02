import router from 'umi/router';
import { register } from '@/services/user';
import { setAuthority } from '@/utils/authority';
import { reloadAuthorized } from '@/utils/Authorized';

export default {
  namespace: 'register',

  state: {
    status: undefined,
    message: '',
  },

  effects: {
    *submit({ payload }, { call, put }) {
      const response = yield call(register, payload);
      yield put({
        type: 'registerHandle',
        payload: response,
      });
      if (response && response.status === 'SUCCESS') {
        reloadAuthorized();
        if (response.data.authority === 'admin') {
          yield router.push('/');
        } else {
          yield router.push({
            pathname: '/user/register-result',
            state: {
              account: payload.email,
            },
          });
        }
      }
    },
  },

  reducers: {
    registerHandle(state, { payload }) {
      if (payload && payload.status === 'SUCCESS') {
        setAuthority(payload.data.authority);
      } else {
        setAuthority('guest');
      }
      return {
        ...state,
        status: payload && payload.status,
        message: payload && payload.message,
      };
    },
  },
};
