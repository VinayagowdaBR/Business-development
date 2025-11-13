import React, { useState, useEffect } from 'react';
import { DollarSign, Users, ShoppingCart, TrendingUp } from 'lucide-react';
import StatCard from '../components/dashboard/StatCard';
import ActivityFeed from '../components/dashboard/ActivityFeed';
import ChartCard from '../components/dashboard/ChartCard';
import { organizationAPI } from '../services/api';

const DashboardPage = () => {
  const [orgData, setOrgData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const org = await organizationAPI.getMyOrganization();
      setOrgData(org);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Sample data for charts
  const salesData = [
    { name: 'Jan', value: 4000 },
    { name: 'Feb', value: 3000 },
    { name: 'Mar', value: 5000 },
    { name: 'Apr', value: 4500 },
    { name: 'May', value: 6000 },
    { name: 'Jun', value: 5500 },
  ];

  const revenueData = [
    { name: 'Week 1', value: 12000 },
    { name: 'Week 2', value: 19000 },
    { name: 'Week 3', value: 15000 },
    { name: 'Week 4', value: 25000 },
  ];

  const activities = [
    {
      type: 'success',
      action: 'New user registered',
      time: '2 hours ago',
      description: 'John Doe joined the organization',
    },
    {
      type: 'info',
      action: 'Database updated',
      time: '5 hours ago',
      description: '142 records were synchronized',
    },
    {
      type: 'warning',
      action: 'Payment pending',
      time: '1 day ago',
      description: 'Invoice #1234 requires attention',
    },
    {
      type: 'success',
      action: 'Report generated',
      time: '2 days ago',
      description: 'Monthly sales report is ready',
    },
  ];

  if (loading) {
    return <div style={styles.loading}>Loading dashboard...</div>;
  }

  return (
    <div style={styles.container}>
      {/* Page Header */}
      <div style={styles.pageHeader}>
        <div>
          <h1 style={styles.pageTitle}>Dashboard</h1>
          <p style={styles.pageSubtitle}>Welcome to {orgData?.organization_name}</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={styles.statsGrid}>
        <StatCard
          title="Total Sales"
          value="39,881"
          change="+4.48%"
          changeType="up"
          icon={DollarSign}
          color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        />
        <StatCard
          title="Total Users"
          value={orgData?.user_count || 0}
          change="+2.83%"
          changeType="up"
          icon={Users}
          color="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        />
        <StatCard
          title="Purchases"
          value="42,283"
          change="+2.83%"
          changeType="up"
          icon={ShoppingCart}
          color="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        />
        <StatCard
          title="Orders"
          value="58,470"
          change="+5.15%"
          changeType="up"
          icon={TrendingUp}
          color="linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
        />
      </div>

      {/* Charts and Activity Grid */}
      <div style={styles.chartsGrid}>
        <div style={styles.chartColumn}>
          <ChartCard title="Sales Statistics" data={salesData} type="area" />
        </div>
        <div style={styles.activityColumn}>
          <ActivityFeed activities={activities} />
        </div>
      </div>

      {/* Bottom Chart */}
      <div style={styles.bottomChart}>
        <ChartCard title="Revenue Overview" data={revenueData} type="line" />
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '30px',
    background: '#f8f9fa',
    minHeight: 'calc(100vh - 70px)',
  },
  loading: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    fontSize: '18px',
    color: '#666',
  },
  pageHeader: {
    marginBottom: '30px',
  },
  pageTitle: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#333',
    margin: '0 0 8px 0',
  },
  pageSubtitle: {
    fontSize: '14px',
    color: '#999',
    margin: 0,
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '30px',
  },
  chartsGrid: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr',
    gap: '20px',
    marginBottom: '30px',
  },
  chartColumn: {
    gridColumn: '1',
  },
  activityColumn: {
    gridColumn: '2',
  },
  bottomChart: {
    marginBottom: '30px',
  },
};

export default DashboardPage;
