import React from "react";
import isoFetch from "isomorphic-unfetch";
import Link from "next/link";
import { useRouter } from "next/router";
import { Menu, Container } from "semantic-ui-react";
import useUser from "../lib/useUser";

const Header: React.FC = () => {
  const { user, mutateUser } = useUser();

  const router = useRouter();
  const matches: (pathname: string) => boolean = (pathname) =>
    router.pathname === pathname;
  const startsWith: (pathname: string) => boolean = (pathname) =>
    router.pathname.startsWith(pathname);

  const logout = async (e: React.SyntheticEvent) => {
    e.preventDefault();

    try {
      const res = await isoFetch(`/api/logout`);
      mutateUser();
    } catch (error) {
      console.error(error);
      alert(error);
    }
  };

  return (
    <nav>
      <Menu style={{ marginBottom: "4em" }} size="large" color="green" inverted>
        <Container>
          <Link href="/">
            <Menu.Item header style={{ fontSize: "20px" }}>
              🔐 Cryptomato 🍅
            </Menu.Item>
          </Link>
          <Link href="/challenges">
            <Menu.Item name="challenges" active={startsWith("/challenges")} />
          </Link>
          <Link href="/submissions">
            <Menu.Item name="submissions" active={startsWith("/submissions")} />
          </Link>
          {user.isLoggedIn && (
            <Menu.Menu position="right">
              <Menu.Item name="logout" onClick={logout} />
            </Menu.Menu>
          )}
        </Container>
      </Menu>
    </nav>
  );
};

export default Header;
