function MainLayout({ sidebar, children, insights }) {
  return (
    <div className="app-layout">
      {sidebar}
      <main className="app-main">{children}</main>
      {insights}
    </div>
  );
}

export default MainLayout;
