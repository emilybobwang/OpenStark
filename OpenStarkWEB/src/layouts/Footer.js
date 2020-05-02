import React, { Fragment } from 'react';
import { Layout, Icon } from 'antd';
import GlobalFooter from '@/components/GlobalFooter';

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1054356_ka12c4y9rgk.js',
});
const { Footer } = Layout;
const FooterView = () => (
  <Footer style={{ padding: 0 }}>
    <GlobalFooter
      links={[
        {
          key: 'blog',
          title: <IconFont type="icon-wordpress" />,
          href: 'https://www.bstester.com/',
          blankTarget: true,
        },
        {
          key: 'github',
          title: <Icon type="github" />,
          href: 'https://github.com/BSTester',
          blankTarget: true,
        },
      ]}
      copyright={
        <Fragment>
          Copyright&nbsp;&nbsp;
          <Icon type="copyright" />
          2018-{new Date().getFullYear()}&nbsp;&nbsp;鸥鹏斯塔克
        </Fragment>
      }
    />
  </Footer>
);
export default FooterView;
