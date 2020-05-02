import React, { Component } from 'react';
import { connect } from 'dva';
import { Card } from 'antd';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import IFrame from './IFrame';

@connect()
class Deploy extends Component {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'global/changeLayoutCollapsed',
      payload: true,
    });
  }

  render() {
    const { match } = this.props;
    const src = match.path.includes('datamart')
      ? 'http://172.20.20.160:8081/structure'
      : 'http://172.20.20.160:8030/testproject/publish/list';
    return (
      <PageHeaderWrapper>
        <Card>
          <IFrame {...this.props} src={src} />
        </Card>
      </PageHeaderWrapper>
    );
  }
}

export default Deploy;
