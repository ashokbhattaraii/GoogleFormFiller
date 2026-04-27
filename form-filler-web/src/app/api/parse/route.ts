import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { url } = await req.json();

    if (!url || !url.startsWith('https://docs.google.com/forms/')) {
      return NextResponse.json({ error: 'Invalid Google Form URL' }, { status: 400 });
    }

    const response = await fetch(url);
    const html = await response.text();

    const match = html.match(/var FB_PUBLIC_LOAD_DATA_ = (\[[\s\S]*?\]);\s*<\/script>/);
    if (!match) {
      return NextResponse.json({ error: 'Could not parse form data. Make sure the form is public.' }, { status: 400 });
    }

    const data = JSON.parse(match[1]);
    const items = data[1][1];

    // Extract form posting url
    // Usually it's https://docs.google.com/forms/d/e/<FORM_ID>/formResponse
    // data[14] has the form ID string usually
    let formId = data[14] || url.match(/\/d\/e\/([^\/]+)/)?.[1];
    if (formId && formId.startsWith('e/')) {
      formId = formId.substring(2);
    }
    const postUrl = `https://docs.google.com/forms/d/e/${formId}/formResponse`;

    // fbzx
    const fbzxMatch = html.match(/name="fbzx" value="([^"]+)"/);
    const fbzx = fbzxMatch ? fbzxMatch[1] : '';

    // pageHistory
    const pageHistoryMatch = html.match(/name="pageHistory" value="([^"]+)"/);
    const pageHistory = pageHistoryMatch ? pageHistoryMatch[1] : '0';

    const fields = [];

    for (const item of items) {
      const type = item[3];
      // 8 is page break, 9 is title, etc.
      if (type === 8 || type === 9 || type === 11) continue;

      const title = item[1];
      if (!title) continue;

      if (item[4] && item[4].length > 0) {
        const subItem = item[4][0];
        const id = subItem[0];
        const required = subItem[2] === 1;

        let options = [];
        if (subItem[1] && Array.isArray(subItem[1])) {
          options = subItem[1].map((o: any) => o[0]).filter(Boolean);
        }

        fields.push({
          id,
          title: title.trim(),
          type, // 0=Short, 1=Paragraph, 2=Radio, 3=Dropdown, 4=Checkbox, 5=Scale
          options,
          required
        });
      }
    }

    return NextResponse.json({
      title: data[3] || data[1][0] || 'Google Form',
      postUrl,
      fbzx,
      pageHistory,
      fields
    });

  } catch (error: any) {
    console.error(error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
