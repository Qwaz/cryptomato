import React, { ReactNode } from "react";
import Header from "./Header";
import Footer from "./Footer";
import { Segment } from "semantic-ui-react";

type Props = {
  children: ReactNode;
};

const Layout: React.FC<Props> = (props) => (
  <div>
    <Header />
    {props.children}
    <Footer />
  </div>
);

export default Layout;
