import type { LegalSource, ExampleQuestion, ChatMessage, RagStep } from '@/types';

export const EXAMPLE_QUESTIONS: ExampleQuestion[] = [
  {
    id: 'q1',
    question: 'How are citizens of Gulf Cooperative Council (GCC) States treated when practicing economic activities and professions in the State?',
    category: 'Corporate Law',
    icon: 'Building2',
  },
  {
    id: 'q2',
    question: 'What are the exceptions to the equal treatment of GCC State citizens regarding economic activities and professions in the State?',
    category: 'Labor Law',
    icon: 'Users',
  },
  {
    id: 'q3',
    question: 'What obligation is outlined regarding the treatment of creditors with claims of the same nature?',
    category: 'Investment Law',
    icon: 'TrendingUp',
  },
  {
    id: 'q4',
    question: 'What are the VAT registration thresholds and obligations in the UAE?',
    category: 'Tax Law',
    icon: 'Receipt',
  },
];

const SOURCES: Record<string, LegalSource> = {
  company_law: {
    id: 'src_company_law',
    lawName: 'Federal Decree-Law No. 32 of 2021 on Commercial Companies',
    lawNumber: '32',
    year: 2021,
    articleNumber: 'Article 10',
    articleTitle: 'Establishment of Companies in Free Zones',
    relevantText:
      'A company established in a Free Zone shall be subject to the provisions of this Decree-Law unless the Authority of the Free Zone issues special provisions regulating the establishment and incorporation of companies therein.',
    fullArticleText: `Article 10 — Establishment of Companies in Free Zones

1. A company established in a Free Zone shall be subject to the provisions of this Decree-Law unless the Authority of the Free Zone issues special provisions regulating the establishment and incorporation of companies therein.

2. The establishment of a company in a Free Zone shall require approval from the competent authority of that Free Zone, which shall verify compliance with all applicable regulations, including capital requirements, ownership structures, and permitted activities.

3. Free Zone companies may be wholly owned by foreign investors and shall enjoy the benefits and incentives provided under the applicable Free Zone regulations.

4. Each Free Zone authority shall maintain a register of all companies incorporated within its jurisdiction and shall provide the Ministry of Economy with periodic reports on company registrations.

5. Notwithstanding the provisions of this Article, Free Zone companies conducting activities in the mainland of the State shall be subject to the applicable mainland regulations and licensing requirements.`,
    relevanceScore: 0.94,
    category: 'Corporate Law',
    jurisdiction: 'Federal',
  },
  free_zone_reg: {
    id: 'src_free_zone_reg',
    lawName: 'Cabinet Decision No. 55 of 2021 — Free Zone Regulations',
    lawNumber: '55',
    year: 2021,
    articleNumber: 'Article 7',
    articleTitle: 'Licensing Requirements for Free Zone Establishments',
    relevantText:
      'Any person intending to establish a business in a Free Zone shall submit an application to the Free Zone Authority, including a business plan, proof of capital, and identification documents of shareholders and directors.',
    fullArticleText: `Article 7 — Licensing Requirements for Free Zone Establishments

1. Any person intending to establish a business in a Free Zone shall submit an application to the Free Zone Authority, including a business plan, proof of capital, and identification documents of shareholders and directors.

2. The Free Zone Authority shall review the application and issue a license within fifteen (15) working days from the date of submission of a complete application.

3. The minimum capital requirement shall be determined by each Free Zone Authority based on the nature of the business activity, provided that such requirements shall not be less than the minimums prescribed by the Ministry of Economy.

4. A Free Zone license shall be valid for one (1) year and shall be renewable subject to compliance with all applicable regulations and payment of prescribed fees.

5. The Free Zone Authority may suspend or revoke a license if the licensee violates any provision of the applicable regulations or engages in activities outside the scope of the license.`,
    relevanceScore: 0.89,
    category: 'Corporate Law',
    jurisdiction: 'Federal',
  },
  fdi_law: {
    id: 'src_fdi_law',
    lawName: 'Federal Decree-Law No. 26 of 2020 on Foreign Direct Investment',
    lawNumber: '26',
    year: 2020,
    articleNumber: 'Article 5',
    articleTitle: 'Permitted Sectors for Foreign Investment',
    relevantText:
      'Foreign investors may invest in the State in the form of a foreign company, or through the incorporation of a company subject to the Commercial Companies Law, in sectors included in the list of activities permitted for foreign direct investment.',
    fullArticleText: `Article 5 — Permitted Sectors for Foreign Investment

1. Foreign investors may invest in the State in the form of a foreign company, or through the incorporation of a company subject to the Commercial Companies Law, in sectors included in the list of activities permitted for foreign direct investment.

2. The Cabinet, upon the proposal of the Minister of Economy and the recommendation of the Foreign Direct Investment Committee, shall issue a decision determining the activities, sectors, and percentage of foreign ownership permitted.

3. The list of permitted activities shall be reviewed periodically, taking into account economic development priorities, sectoral strategies, and international obligations.

4. Foreign investors enjoying the benefits of international treaties to which the State is a party shall be treated in accordance with the provisions of such treaties.

5. The investor shall comply with all environmental, health, safety, and technical standards applicable in the State.`,
    relevanceScore: 0.72,
    category: 'Investment Law',
    jurisdiction: 'Federal',
  },
  labor_law: {
    id: 'src_labor_law',
    lawName: 'Federal Decree-Law No. 33 of 2021 on the Regulation of Labour Relations',
    lawNumber: '33',
    year: 2021,
    articleNumber: 'Article 51',
    articleTitle: 'End-of-Service Gratuity',
    relevantText:
      'A full-time foreign worker who has completed one (1) year or more in continuous service shall be entitled to end-of-service gratuity upon the termination of service, calculated based on the last basic wage.',
    fullArticleText: `Article 51 — End-of-Service Gratuity

1. A full-time foreign worker who has completed one (1) year or more in continuous service shall be entitled to end-of-service gratuity upon the termination of service, calculated based on the last basic wage as follows:
   a. Twenty-one (21) days' wage for each year of the first five (5) years of service;
   b. Thirty (30) days' wage for each year exceeding such period.

2. The aggregate gratuity shall not exceed the aggregate wage of two (2) years.

3. Days of absence from work without pay shall not be included in the calculation of the period of service.

4. If the worker terminates the contract before completing five (5) years of service, the worker shall be entitled to gratuity calculated in accordance with the provisions of the implementing regulations of this Decree-Law.

5. The employer may deduct from the gratuity any amounts owed by the worker under the law or the employment contract, provided that the worker has been given the opportunity to respond to such claims.

6. In the event of the worker's death, the gratuity shall be paid to the worker's beneficiaries.`,
    relevanceScore: 0.91,
    category: 'Labor Law',
    jurisdiction: 'Federal',
  },
  labor_exec: {
    id: 'src_labor_exec',
    lawName: 'Cabinet Decision No. 1 of 2022 — Executive Regulations of the Labour Relations Law',
    lawNumber: '1',
    year: 2022,
    articleNumber: 'Article 32',
    articleTitle: 'Calculation of End-of-Service Gratuity',
    relevantText:
      'The end-of-service gratuity shall be calculated on the basis of the last basic wage of the worker, excluding allowances, bonuses, and other variable components of the wage.',
    fullArticleText: `Article 32 — Calculation of End-of-Service Gratuity

1. The end-of-service gratuity shall be calculated on the basis of the last basic wage of the worker, excluding allowances, bonuses, and other variable components of the wage.

2. The daily wage for the purposes of gratuity calculation shall be the basic wage divided by the number of working days in the year as per the employment contract.

3. Where the worker is employed on a piece-rate or commission basis, the gratuity shall be calculated on the average wage earned during the last three (3) months of service.

4. The gratuity shall be paid to the worker within fourteen (14) days from the date of termination of the employment relationship.

5. If the employer fails to pay the gratuity within the prescribed period, the employer shall be liable for any additional amounts as determined by the competent authority.`,
    relevanceScore: 0.86,
    category: 'Labor Law',
    jurisdiction: 'Federal',
  },
  vat_law: {
    id: 'src_vat_law',
    lawName: 'Federal Decree-Law No. 8 of 2017 on Value Added Tax',
    lawNumber: '8',
    year: 2017,
    articleNumber: 'Article 50',
    articleTitle: 'Registration Threshold',
    relevantText:
      'A Person shall register for Tax if the total value of the Taxable Supplies and Imports made by the Person exceeds the Mandatory Registration Threshold of Three Hundred and Seventy-Five Thousand Dirhams (AED 375,000).',
    fullArticleText: `Article 50 — Registration Threshold

1. A Person shall register for Tax if the total value of the Taxable Supplies and Imports made by the Person exceeds the Mandatory Registration Threshold of Three Hundred and Seventy-Five Thousand Dirhams (AED 375,000) in the preceding twelve (12) months, or where the Person anticipates that the total value of Taxable Supplies will exceed the Mandatory Registration Threshold in the next thirty (30) days.

2. A Person may voluntarily register for Tax if the total value of the Taxable Supplies and Imports exceeds the Voluntary Registration Threshold of One Hundred and Eighty-Seven Thousand Five Hundred Dirhams (AED 187,500) in the preceding twelve (12) months.

3. The registration shall be effective from the date determined by the Authority.

4. A registered Person shall issue Tax Invoices in accordance with the provisions of this Decree-Law and the Executive Regulations.

5. A registered Person shall file Tax Returns and pay the Tax due to the Authority within the periods prescribed by the Executive Regulations.`,
    relevanceScore: 0.93,
    category: 'Tax Law',
    jurisdiction: 'Federal',
  },
  vat_exec: {
    id: 'src_vat_exec',
    lawName: 'Cabinet Decision No. 52 of 2017 — Executive Regulations of the VAT Law',
    lawNumber: '52',
    year: 2017,
    articleNumber: 'Article 11',
    articleTitle: 'Obligations of Registered Persons',
    relevantText:
      'A Registrant shall maintain accounting records and Tax Invoices for a period of at least five (5) years from the end of the Tax Period to which they relate.',
    fullArticleText: `Article 11 — Obligations of Registered Persons

1. A Registrant shall maintain accounting records and Tax Invoices for a period of at least five (5) years from the end of the Tax Period to which they relate.

2. A Registrant shall file a Tax Return for each Tax Period, whether or not any Tax is due, within twenty-eight (28) days from the end of the Tax Period.

3. A Registrant shall pay the Tax due to the Authority's bank account as specified in the Tax Return.

4. A Registrant shall notify the Authority of any change in its address, contact details, or business activity within twenty (20) working days of such change.

5. A Registrant shall display its Tax Registration Number on all Tax Invoices and official correspondence.`,
    relevanceScore: 0.81,
    category: 'Tax Law',
    jurisdiction: 'Federal',
  },
};

const RESPONSES: { keywords: string[]; content: string; sourceIds: string[] }[] = [
  {
    keywords: ['free zone', 'company', 'establish', 'corporate', 'business setup'],
    content: `## Establishing a Company in a UAE Free Zone

Setting up a company in a UAE free zone offers **100% foreign ownership**, tax exemptions, and streamlined licensing. Here's what you need to know:

### Key Requirements

1. **Approval from the Free Zone Authority** — You must submit an application including a business plan, proof of capital, and identification documents for all shareholders and directors.

2. **Licensing** — The Free Zone Authority reviews your application and issues a license within **15 working days** of receiving a complete application.

3. **Capital Requirements** — Minimum capital varies by Free Zone and business activity, but cannot be less than the minimums prescribed by the Ministry of Economy.

4. **Legal Framework** — Free Zone companies are governed by the **Commercial Companies Law** unless the Free Zone Authority issues its own special provisions.

### Important Considerations

- Free Zone licenses are valid for **one year** and must be renewed annually
- Companies conducting activities in the mainland are subject to mainland regulations
- Each Free Zone maintains its own register of incorporated companies

> **Note:** While Free Zone companies enjoy significant benefits, activities outside the Free Zone boundaries may require additional mainland licensing.`,
    sourceIds: ['company_law', 'free_zone_reg', 'fdi_law'],
  },
  {
    keywords: ['labor', 'employee', 'gratuity', 'end of service', 'worker', 'employment'],
    content: `## End-of-Service Gratuity Under UAE Labour Law

Under **Federal Decree-Law No. 33 of 2021**, full-time foreign workers who complete at least one year of continuous service are entitled to end-of-service gratuity upon termination.

### Calculation Method

The gratuity is based on the **last basic wage** (excluding allowances and bonuses):

| Service Period | Gratuity Rate |
|---|---|
| First 5 years | **21 days** of wage per year |
| After 5 years | **30 days** of wage per year |

### Key Points

- The **total gratuity cannot exceed 2 years' worth of wages**
- Unpaid leave days are **excluded** from the calculation
- Gratuity must be paid within **14 days** of termination
- Employers may deduct amounts owed by the worker (after giving the worker a chance to respond)
- In case of the worker's death, gratuity goes to beneficiaries

### Calculation Example

For a worker earning AED 10,000/month basic salary after 7 years of service:

- **First 5 years:** 21 days × 5 = 105 days
- **Next 2 years:** 30 days × 2 = 60 days
- **Total:** 165 days of basic wage

> The daily wage is calculated as basic salary ÷ working days in the year as per the employment contract.`,
    sourceIds: ['labor_law', 'labor_exec'],
  },
  {
    keywords: ['vat', 'tax', 'registration', 'threshold', 'value added'],
    content: `## VAT Registration in the UAE

The UAE introduced Value Added Tax (VAT) at a standard rate of **5%** under Federal Decree-Law No. 8 of 2017.

### Registration Thresholds

| Type | Threshold |
|---|---|
| **Mandatory** | AED 375,000 |
| **Voluntary** | AED 187,500 |

### When to Register

**Mandatory registration** applies if:
- Your taxable supplies exceeded AED 375,000 in the past 12 months, **or**
- You anticipate exceeding AED 375,000 in the next 30 days

**Voluntary registration** is available if your taxable supplies exceed AED 187,500 in the past 12 months.

### Ongoing Obligations

1. **Tax Returns** — File for each tax period within **28 days** of period end
2. **Record Keeping** — Maintain accounting records and tax invoices for **at least 5 years**
3. **Tax Invoices** — Must be issued for all taxable supplies
4. **Changes** — Notify the FTA of any changes within **20 working days**

> Failure to register when required or to file returns on time can result in penalties under the tax legislation.`,
    sourceIds: ['vat_law', 'vat_exec'],
  },
  {
    keywords: ['foreign', 'investment', 'fdi', 'mainland'],
    content: `## Foreign Direct Investment in the UAE Mainland

The UAE's **Federal Decree-Law No. 26 of 2020** regulates foreign direct investment, significantly liberalizing ownership rules for mainland companies.

### Key Provisions

1. **Permitted Sectors** — The Cabinet determines which activities and sectors permit foreign investment and the allowed ownership percentages, based on economic priorities.

2. **Investment Forms** — Foreign investors may invest through a foreign company branch or by incorporating a company under the Commercial Companies Law.

3. **International Treaties** — Investors from countries with treaty arrangements with the UAE receive treatment under those treaty provisions.

### Regulatory Framework

- The **Foreign Direct Investment Committee** recommends permitted activities to the Cabinet
- The list of permitted activities is **reviewed periodically**
- Investors must comply with all **environmental, health, safety, and technical standards**

> Following the 2021 amendments to the Commercial Companies Law, most mainland activities now allow 100% foreign ownership, though certain strategic impact activities retain restrictions.`,
    sourceIds: ['fdi_law', 'company_law'],
  },
];

function findResponse(query: string): { content: string; sourceIds: string[] } {
  const lower = query.toLowerCase();
  for (const r of RESPONSES) {
    if (r.keywords.some((k) => lower.includes(k))) {
      return { content: r.content, sourceIds: r.sourceIds };
    }
  }
  // Default response
  return {
    content: `## Legal Research Results

I've analyzed your query against UAE federal legislation. Here's what I found:

Based on the available legal database, your question touches on several areas of UAE law. The most relevant provisions are referenced below in the **Sources Used** section.

### Summary

The UAE legal framework provides comprehensive regulation across commercial, labor, tax, and investment domains. Each area is governed by specific federal decree-laws and their corresponding executive regulations.

> For specific legal advice tailored to your situation, please consult with a licensed UAE legal practitioner.`,
    sourceIds: ['company_law', 'free_zone_reg'],
  };
}

export function getMockResponse(query: string): { content: string; sources: LegalSource[]; ragSteps: RagStep[] } {
  const { content, sourceIds } = findResponse(query);
  const sources = sourceIds.map((id) => SOURCES[id]).filter(Boolean);
  const ragSteps = buildRagSteps(query, sources);
  return { content, sources, ragSteps };
}

function buildRagSteps(query: string, sources: LegalSource[]): RagStep[] {
  // All potential docs for retrieval demonstration
  const allDocs = Object.values(SOURCES);
  const retrievedDocs = allDocs.slice(0, 6);
  const topK = retrievedDocs.slice(0, 4);
  const reranked = sources.length > 0 ? sources : topK.slice(0, 2);

  return [
    {
      label: 'Query Processing',
      description: 'Parsing and embedding the user query',
      duration: '0.12s',
      items: [
        {
          id: 'q1',
          title: 'Query Embedding',
          subtitle: `"${query.length > 50 ? query.slice(0, 50) + '...' : query}"`,
          metadata: '768-dim vector · cosine similarity',
        },
      ],
    },
    {
      label: 'Retrieved Documents',
      description: 'Vector search across legislation corpus',
      duration: '0.34s',
      items: retrievedDocs.map((doc, i) => ({
        id: `ret_${doc.id}`,
        title: `${doc.lawName}`,
        subtitle: `${doc.articleNumber} — ${doc.articleTitle}`,
        score: 0.5 + Math.random() * 0.35,
        metadata: `Chunk ${i + 1} · ${doc.category}`,
      })),
    },
    {
      label: 'Top-K Selection',
      description: 'K=4 highest scoring chunks',
      duration: '0.02s',
      items: topK.map((doc, i) => ({
        id: `topk_${doc.id}`,
        title: `${doc.lawName}`,
        subtitle: `${doc.articleNumber}`,
        score: 0.7 + Math.random() * 0.2,
        metadata: `Rank ${i + 1}`,
      })),
    },
    {
      label: 'Reranked Results',
      description: 'Cross-encoder reranking for precision',
      duration: '0.45s',
      items: reranked.map((doc, i) => ({
        id: `rr_${doc.id}`,
        title: `${doc.lawName}`,
        subtitle: `${doc.articleNumber} — ${doc.articleTitle}`,
        score: doc.relevanceScore,
        metadata: `Final Rank ${i + 1}`,
      })),
    },
    {
      label: 'Final Context',
      description: 'Context window assembly for generation',
      duration: '0.08s',
      items: reranked.map((doc) => ({
        id: `ctx_${doc.id}`,
        title: `${doc.articleNumber}`,
        subtitle: `${doc.lawName}`,
        metadata: `${doc.relevantText.length} chars`,
      })),
    },
  ];
}

export function generateMessageId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export function generateConversationId(): string {
  return `conv_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export function createMockMessages(): ChatMessage[] {
  return [];
}
