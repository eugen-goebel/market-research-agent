"""
Mock data for --dry-run mode.

Provides a realistic AnalysisResult for SAP SE so the full pipeline
(report generation, DOCX output, styling) can be tested without an API key.
"""

from .analyst import AnalysisResult, SWOTAnalysis, Competitor


SAP_MOCK = AnalysisResult(
    executive_summary=(
        "SAP SE is the world's leading provider of enterprise application software, "
        "with over 400,000 customers in 180 countries. The company has successfully "
        "pivoted from on-premise ERP to a cloud-first model, with cloud revenue now "
        "representing over 40% of total sales. Despite intense competition from Oracle "
        "and Salesforce, SAP maintains a dominant position in core ERP, with its S/4HANA "
        "platform driving a multi-year migration cycle across its installed base."
    ),
    company_overview=(
        "SAP SE was founded in 1972 in Walldorf, Germany, by five former IBM engineers. "
        "Today, headquartered in Walldorf, Baden-Württemberg, it employs over 105,000 people "
        "worldwide and generates approximately €31 billion in annual revenue. SAP's product "
        "portfolio spans ERP (S/4HANA), CRM (Salesforce competitor: SAP CX), supply chain "
        "(SAP IBP), HR management (SuccessFactors), and business intelligence (SAP Analytics "
        "Cloud). The company serves large enterprises and mid-market companies across "
        "manufacturing, retail, financial services, and the public sector."
    ),
    market_position=(
        "SAP holds a commanding ~24% share of the global ERP market and is widely regarded "
        "as the system of record for core business processes at Fortune 500 companies. Its "
        "competitive moat stems from deep integration complexity — replacing SAP is a "
        "multi-year, high-risk transformation that most enterprises avoid. SAP's RISE with SAP "
        "offering bundles S/4HANA Cloud with managed services, accelerating cloud migration. "
        "The company targets €21.5 billion in cloud revenue by 2025, indicating a fundamental "
        "shift in its business model toward recurring subscription income."
    ),
    swot=SWOTAnalysis(
        strengths=[
            "Dominant ERP market share (~24%) with extremely high switching costs",
            "400,000+ customer installed base providing stable recurring revenue",
            "Deep industry-specific solutions across 25+ verticals",
            "Strong R&D investment (~15% of revenue) driving continuous innovation",
            "Successful RISE with SAP cloud migration program gaining traction",
        ],
        weaknesses=[
            "Legacy on-premise revenue declining faster than cloud growth can compensate",
            "Complex, expensive implementation projects averaging 18–24 months",
            "User experience historically criticized as outdated compared to modern SaaS",
            "Dependence on partner ecosystem for delivery creates quality inconsistency",
            "SAP Business Suite to S/4HANA migration creates customer anxiety and churn risk",
        ],
        opportunities=[
            "Generative AI integration (Joule AI assistant) across entire product suite",
            "Untapped mid-market segment via SAP Business ByDesign and partner channels",
            "Supply chain digitalization demand accelerating post-COVID across all industries",
            "Green Ledger sustainability reporting becoming mandatory (CSRD, EU taxonomy)",
            "Business Network (Ariba, Fieldglass) expanding into B2B marketplace model",
        ],
        threats=[
            "Oracle Fusion Cloud aggressively winning SAP displacement deals",
            "Salesforce + MuleSoft offering compelling alternative for CRM + integration",
            "Microsoft Dynamics 365 gaining share in mid-market with Teams integration",
            "AI-native ERP startups (e.g., Workday for HCM) reducing SAP's edge in niches",
            "Macro slowdown delaying large transformation projects and license upgrades",
        ],
    ),
    top_competitors=[
        Competitor(
            name="Oracle Corporation",
            overview="US-based enterprise software giant offering Oracle Fusion Cloud ERP, HCM, and SCM as direct SAP competitors.",
            key_strength="Integrated technology stack (database + cloud infrastructure + applications) and aggressive cloud pricing",
            key_weakness="Perceived as complex to implement and historically reliant on hardware bundling",
        ),
        Competitor(
            name="Microsoft Dynamics 365",
            overview="Microsoft's ERP and CRM suite tightly integrated with Azure, Teams, and the Microsoft 365 ecosystem.",
            key_strength="Seamless integration with Office 365 and Azure, plus competitive mid-market pricing",
            key_weakness="Limited depth for large enterprise manufacturing and complex logistics scenarios",
        ),
        Competitor(
            name="Salesforce",
            overview="World's leading CRM platform, increasingly competing with SAP CX and expanding into ERP adjacencies via MuleSoft and Slack.",
            key_strength="Best-in-class CRM UX, massive AppExchange ecosystem, and AI (Einstein) leadership",
            key_weakness="Limited ERP core capabilities; relies on integrations for back-office processes",
        ),
        Competitor(
            name="Workday",
            overview="Cloud-native HCM and financial management platform targeting SAP SuccessFactors and SAP S/4HANA Finance.",
            key_strength="Modern cloud-native architecture, strong user adoption, and best-of-breed HR analytics",
            key_weakness="Narrower industry coverage than SAP; limited manufacturing and supply chain capabilities",
        ),
    ],
    key_trends=[
        "Generative AI embedded in ERP workflows: co-pilots, automated reconciliation, predictive maintenance",
        "Cloud ERP migration accelerating — Gartner forecasts 75% of ERP workloads in cloud by 2026",
        "Sustainability reporting mandates (EU CSRD, SEC climate disclosure) driving demand for ESG modules",
        "Supply chain resilience investments post-COVID boosting SCM and procurement software spend",
        "Rise of composable ERP: modular best-of-breed architectures challenging monolithic suites",
        "Low-code / no-code customization tools reducing dependency on expensive SI partners",
        "Data sovereignty and localization requirements (GDPR, China PIPL) shaping cloud deployment strategies",
    ],
    investment_thesis=(
        "SAP's multi-year cloud transition is approaching an inflection point, with RISE with SAP "
        "driving high-value migrations from the 400,000-strong installed base. If the company "
        "successfully embeds generative AI (Joule) across its suite and accelerates mid-market "
        "adoption, it is well-positioned to sustain double-digit cloud revenue growth while "
        "expanding operating margins as the mix shifts from license to subscription."
    ),
    risk_factors=[
        "Cloud transition cannibilizes high-margin license revenue faster than expected",
        "Oracle or Microsoft displacing SAP in key enterprise accounts during migration windows",
        "Global recession delaying large-scale ERP transformation projects by 12–24 months",
        "Integration failures or cost overruns in RISE with SAP eroding customer trust",
        "Talent competition for AI and cloud engineers increasing R&D cost base",
    ],
)
