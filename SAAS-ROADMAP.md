# WIGEON SaaS Platform - Product Roadmap 🦆

## Vision Statement

Transform WIGEON from a single-user CLI tool into a **multi-tenant SaaS platform** where users can automatically track, consolidate, and analyze reports from third-party vendors through email integrations.

**Tagline**: "Never lose track of vendor reports again."

---

## Current State (March 2026)

### ✅ What We Have
- **CLI Tool**: Fully functional command-line data integration agent
- **Web Dashboard**: Beautiful Dropbox-style UI for data visualization
- **Data Processing**: Excel, XML, ZIP file parsing
- **Database**: SQLite backend with flexible schema
- **Export Capabilities**: CSV, JSON, Excel exports
- **Real Data**: 39,814 rows of CEVA logistics data ingested

### ⚠️ Current Limitations
- Single-user only (local database)
- Manual file ingestion required
- No user authentication
- No cloud hosting
- Gmail extension blocked (keychain issues)

---

## Product Roadmap

### Phase 1: Shareable Dashboard (Current - Week 1)

**Goal**: Deploy current dashboard for team sharing

**Tasks**:
- [x] Create Dropbox-style UI
- [x] Single HTML file with embedded data
- [ ] Deploy to Blockcell
- [ ] Share URL with stakeholders
- [ ] Gather user feedback
- [ ] Document usage patterns

**Success Metrics**:
- 5+ team members using dashboard
- Positive feedback on UI/UX
- Feature requests collected

**Timeline**: 1 week

---

### Phase 2: Multi-User Foundation (Months 1-2)

**Goal**: Build authentication and user isolation

#### 2.1 User Authentication
- [ ] User registration (email/password)
- [ ] Login/logout functionality
- [ ] Password reset flow
- [ ] Email verification
- [ ] Session management (JWT tokens)

#### 2.2 Database Architecture
- [ ] PostgreSQL setup (multi-tenant)
- [ ] User table schema
- [ ] Workspace/organization model
- [ ] Data isolation per user
- [ ] Migration from SQLite

#### 2.3 Backend API
- [ ] RESTful API (Node.js/Express or Python/FastAPI)
- [ ] User CRUD operations
- [ ] Authentication middleware
- [ ] Rate limiting
- [ ] API documentation (Swagger)

**Success Metrics**:
- 10+ registered users
- Zero data leakage between users
- API response time < 200ms

**Timeline**: 2 months

---

### Phase 3: Automated Data Ingestion (Months 3-4)

**Goal**: Automatic email monitoring and report ingestion

#### 3.1 Gmail Integration
- [ ] Gmail OAuth 2.0 setup
- [ ] Email search automation
- [ ] Attachment download
- [ ] File type detection
- [ ] Error handling and retries

#### 3.2 Background Processing
- [ ] Job queue (Celery/Bull)
- [ ] Scheduled email checks (every hour)
- [ ] File parsing workers
- [ ] Database ingestion pipeline
- [ ] Notification system

#### 3.3 Onboarding Wizard
- [ ] Step 1: Connect Gmail account
- [ ] Step 2: Configure vendor email addresses
- [ ] Step 3: Set report types and patterns
- [ ] Step 4: Test connection
- [ ] Step 5: Review first ingested reports

**User Flow**:
```
1. User signs up
2. User prompted: "Which vendors do you want to track?"
   - Input: "CEVA Logistics, Acme Corp"
3. User prompted: "What email addresses send reports?"
   - Input: "ops_reporting@example.com, vendor@acme.com"
4. User prompted: "How often should we check?"
   - Options: Hourly, Daily, Weekly
5. WIGEON connects to Gmail and starts monitoring
6. User sees dashboard populate automatically
```

**Success Metrics**:
- 80% of users complete onboarding
- 95% successful email connections
- Average 10 reports ingested per user

**Timeline**: 2 months

---

### Phase 4: Enhanced Dashboard (Months 5-6)

**Goal**: Real-time updates and advanced features

#### 4.1 Real-Time Updates
- [ ] WebSocket integration
- [ ] Live dashboard updates
- [ ] Notification badges
- [ ] Activity feed

#### 4.2 Advanced Features
- [ ] Search and filtering
- [ ] Date range picker
- [ ] Custom report views
- [ ] Data drill-down
- [ ] Interactive charts (Chart.js/D3.js)

#### 4.3 Export Enhancements
- [ ] Scheduled exports
- [ ] Email delivery of exports
- [ ] Custom export templates
- [ ] API access for exports

#### 4.4 Mobile Optimization
- [ ] Responsive design refinement
- [ ] Touch-friendly interactions
- [ ] Mobile app (PWA)

**Success Metrics**:
- 90% user satisfaction score
- 50% daily active users
- Average 5 exports per user per week

**Timeline**: 2 months

---

### Phase 5: Enterprise Features (Months 7-9)

**Goal**: Team collaboration and advanced analytics

#### 5.1 Team Workspaces
- [ ] Organization accounts
- [ ] Team member invitations
- [ ] Role-based access control
- [ ] Shared dashboards
- [ ] Collaborative annotations

#### 5.2 Advanced Analytics
- [ ] Trend analysis
- [ ] Anomaly detection
- [ ] Predictive insights
- [ ] Custom metrics
- [ ] Report comparisons

#### 5.3 Integrations
- [ ] Slack notifications
- [ ] Email alerts
- [ ] Webhook support
- [ ] Zapier integration
- [ ] API for third-party apps

#### 5.4 Compliance & Security
- [ ] SOC 2 compliance
- [ ] Data encryption at rest
- [ ] Audit logs
- [ ] GDPR compliance
- [ ] Data retention policies

**Success Metrics**:
- 5+ enterprise customers
- 100+ users per organization
- 99.9% uptime SLA

**Timeline**: 3 months

---

### Phase 6: Scale & Monetization (Months 10-12)

**Goal**: Growth and revenue generation

#### 6.1 Pricing Tiers
- [ ] **Free**: 1 vendor, 100 reports/month
- [ ] **Pro**: $29/mo - 5 vendors, 1,000 reports/month
- [ ] **Business**: $99/mo - Unlimited vendors, 10,000 reports/month
- [ ] **Enterprise**: Custom pricing - Unlimited + support

#### 6.2 Marketing & Growth
- [ ] Landing page
- [ ] Product demo videos
- [ ] Case studies
- [ ] Blog content
- [ ] SEO optimization

#### 6.3 Customer Success
- [ ] Onboarding support
- [ ] Documentation hub
- [ ] Video tutorials
- [ ] Live chat support
- [ ] Customer feedback loop

#### 6.4 Infrastructure Scaling
- [ ] Load balancing
- [ ] Database sharding
- [ ] CDN for assets
- [ ] Monitoring and alerting
- [ ] Disaster recovery

**Success Metrics**:
- 1,000+ registered users
- $10K+ MRR (Monthly Recurring Revenue)
- 90% customer retention
- NPS score > 50

**Timeline**: 3 months

---

## Technical Architecture

### Frontend Stack
```
- Framework: React or Vue.js
- UI Library: Tailwind CSS (Dropbox-style components)
- State Management: Redux/Vuex
- API Client: Axios
- Charts: Chart.js or D3.js
- Real-time: Socket.io client
```

### Backend Stack
```
- API: Node.js (Express) or Python (FastAPI)
- Database: PostgreSQL (multi-tenant)
- Cache: Redis
- Queue: Celery (Python) or Bull (Node.js)
- Auth: JWT tokens
- Email: Gmail API (OAuth 2.0)
```

### Infrastructure
```
- Hosting: AWS (EC2, RDS, S3) or GCP
- CDN: CloudFront or Cloudflare
- Monitoring: DataDog or New Relic
- Logging: ELK Stack or CloudWatch
- CI/CD: GitHub Actions
- Containers: Docker + Kubernetes
```

### Database Schema (Multi-Tenant)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Organizations table
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    plan VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW()
);

-- User-Organization mapping
CREATE TABLE user_organizations (
    user_id INTEGER REFERENCES users(id),
    organization_id INTEGER REFERENCES organizations(id),
    role VARCHAR(50) DEFAULT 'member',
    PRIMARY KEY (user_id, organization_id)
);

-- Third parties (per organization)
CREATE TABLE third_parties (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Reports (per organization)
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    third_party_id INTEGER REFERENCES third_parties(id),
    report_type VARCHAR(255),
    file_name VARCHAR(255),
    file_size INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    row_count INTEGER,
    ingested_at TIMESTAMP DEFAULT NOW()
);

-- Report data (per organization)
CREATE TABLE report_data (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id),
    row_number INTEGER,
    data JSONB NOT NULL
);

-- Gmail connections (per user)
CREATE TABLE gmail_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Email monitoring rules (per organization)
CREATE TABLE email_rules (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    third_party_id INTEGER REFERENCES third_parties(id),
    from_email VARCHAR(255),
    subject_pattern VARCHAR(255),
    check_frequency VARCHAR(50) DEFAULT 'hourly',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## User Journey

### 1. Sign Up & Onboarding (5 minutes)

**Step 1: Create Account**
```
User visits: https://wigeon.app
Clicks "Get Started"
Enters: Email, Password, Name
Receives: Verification email
Clicks: Verify link
```

**Step 2: Connect Gmail**
```
Prompt: "Connect your Gmail account to start tracking reports"
User clicks: "Connect Gmail"
OAuth flow: Grants WIGEON read-only access
Success: "Gmail connected successfully!"
```

**Step 3: Configure Vendors**
```
Prompt: "Which vendors send you reports?"
User inputs: "CEVA Logistics"
Prompt: "What email address do they use?"
User inputs: "ops_reporting@example.com"
Prompt: "What should we look for in the subject line?"
User inputs: "CEVA CLS NORTAM Reporting"
User clicks: "Add Vendor"
```

**Step 4: Test Connection**
```
WIGEON searches Gmail for matching emails
Shows: "Found 5 emails from CEVA Logistics in the past 7 days"
User clicks: "Import These Reports"
WIGEON downloads attachments and ingests data
Shows: "Successfully imported 5 reports with 2,500 rows"
```

**Step 5: View Dashboard**
```
User redirected to dashboard
Sees: Real-time data from CEVA reports
Explores: Recent reports, export files, statistics
```

### 2. Daily Usage (2 minutes)

**Morning Check**
```
User logs in
Dashboard shows: "3 new reports imported overnight"
User clicks: "View New Reports"
Reviews: Latest inventory transactions
Exports: CSV for analysis
```

**Notification Flow**
```
Email notification: "WIGEON found 2 new CEVA reports"
User clicks: Link to dashboard
Reviews: New data automatically ingested
No manual work required
```

### 3. Advanced Usage (10 minutes)

**Custom Analysis**
```
User searches: "inventory transactions last 30 days"
Filters: By SKU, location, date range
Exports: Custom report to Excel
Schedules: Weekly email delivery
```

**Team Collaboration**
```
User invites: Team member via email
Team member: Gets read-only access
Shares: Dashboard link in Slack
Team discusses: Latest vendor performance
```

---

## Competitive Analysis

### Existing Solutions

**1. Manual Email Management**
- ❌ Time-consuming (30+ min/day)
- ❌ Error-prone
- ❌ No consolidation
- ❌ Hard to analyze trends

**2. Zapier + Google Sheets**
- ✅ Some automation
- ❌ Complex setup
- ❌ Limited data processing
- ❌ No analytics
- 💰 Expensive ($20-100/mo)

**3. Custom Scripts**
- ✅ Flexible
- ❌ Requires coding skills
- ❌ Hard to maintain
- ❌ No UI

### WIGEON Advantages

✅ **Fully Automated** - No manual downloads  
✅ **Smart Parsing** - Handles Excel, XML, ZIP  
✅ **Beautiful UI** - Dropbox-style dashboard  
✅ **Multi-Vendor** - Track unlimited vendors  
✅ **Real-Time** - Automatic updates  
✅ **Affordable** - $29/mo vs $100+ for alternatives  
✅ **No Coding** - Simple setup wizard  
✅ **Team-Ready** - Collaboration features  

---

## Go-to-Market Strategy

### Target Customers

**Primary**: Supply Chain Managers
- Receive daily/weekly reports from 3PLs (CEVA, DHL, FedEx)
- Spend 1-2 hours/day managing vendor emails
- Need consolidated view of inventory, shipments, orders

**Secondary**: Operations Teams
- Track service level agreements
- Monitor vendor performance
- Generate executive reports

**Tertiary**: Finance Teams
- Consolidate invoices from multiple vendors
- Track expenses and payments
- Audit vendor charges

### Marketing Channels

1. **Content Marketing**
   - Blog: "How to automate vendor report tracking"
   - Case study: "How Company X saved 10 hours/week"
   - SEO: "vendor report automation", "3PL reporting"

2. **Product Hunt Launch**
   - Launch video demo
   - Offer lifetime deal for early adopters
   - Gather feedback and testimonials

3. **LinkedIn Outreach**
   - Target supply chain professionals
   - Share automation tips
   - Offer free trial

4. **Partnerships**
   - Integrate with 3PL providers
   - Partner with supply chain consultants
   - Join logistics industry associations

5. **Referral Program**
   - Give 1 month free for referrals
   - Offer team discounts
   - Create ambassador program

---

## Success Metrics (12-Month Goals)

### User Metrics
- 1,000 registered users
- 500 active users (50% activation)
- 200 paying customers (40% conversion)
- 90% user retention (monthly)

### Revenue Metrics
- $10K MRR (Monthly Recurring Revenue)
- $120K ARR (Annual Recurring Revenue)
- $50 CAC (Customer Acquisition Cost)
- $600 LTV (Lifetime Value)
- 12:1 LTV:CAC ratio

### Product Metrics
- 10,000+ reports ingested/month
- 1M+ data rows processed
- 99.9% uptime
- < 200ms API response time
- 90+ NPS score

### Engagement Metrics
- 50% daily active users
- 5 exports per user per week
- 3 vendors tracked per user
- 10 min average session time

---

## Risk Mitigation

### Technical Risks

**Risk**: Gmail API rate limits  
**Mitigation**: Implement exponential backoff, batch requests, cache results

**Risk**: Data privacy concerns  
**Mitigation**: SOC 2 compliance, encryption, clear privacy policy

**Risk**: Scalability issues  
**Mitigation**: Horizontal scaling, database sharding, CDN

**Risk**: Gmail extension dependency  
**Mitigation**: Direct Gmail API integration (OAuth 2.0)

### Business Risks

**Risk**: Low user adoption  
**Mitigation**: Free tier, easy onboarding, strong value prop

**Risk**: High churn rate  
**Mitigation**: Customer success team, regular feature updates

**Risk**: Competitive pressure  
**Mitigation**: Focus on UX, fast iteration, customer feedback

**Risk**: Regulatory compliance  
**Mitigation**: Legal review, GDPR compliance, data retention policies

---

## Next Steps (This Week)

### Immediate Actions
1. ✅ Create Dropbox-style UI (DONE)
2. [ ] Deploy to Blockcell for team testing
3. [ ] Share dashboard URL with 5 stakeholders
4. [ ] Gather feedback on UI/UX
5. [ ] Document feature requests

### Week 2-4
1. [ ] Validate SaaS concept with users
2. [ ] Estimate development costs
3. [ ] Create detailed technical spec
4. [ ] Prototype user authentication
5. [ ] Design database schema

### Month 2-3
1. [ ] Build MVP (auth + basic ingestion)
2. [ ] Beta test with 10 users
3. [ ] Iterate based on feedback
4. [ ] Prepare for public launch

---

## Conclusion

WIGEON has the potential to become the **go-to platform for vendor report automation**. With a beautiful Dropbox-style UI, smart automation, and multi-tenant architecture, we can solve a real pain point for supply chain and operations teams.

**The path forward**:
1. ✅ **Now**: Deploy shareable dashboard
2. **Months 1-2**: Build multi-user foundation
3. **Months 3-4**: Automate email ingestion
4. **Months 5-6**: Enhance dashboard features
5. **Months 7-12**: Scale and monetize

**Let's make vendor report tracking effortless!** 🦆✨

---

**Document Version**: 1.0  
**Last Updated**: March 9, 2026  
**Author**: WIGEON Product Team  
**Status**: Roadmap Draft
